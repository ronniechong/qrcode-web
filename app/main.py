from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import qrcode.image.svg
from io import BytesIO

app = FastAPI(title="QR Code API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _make_svg(data: str, box_size: int, border: int) -> bytes:
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(
        data,
        image_factory=factory,
        box_size=box_size,
        border=border,
    )
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue()


def _make_png(data: str, box_size: int, border: int) -> bytes:
    img = qrcode.make(data, box_size=box_size, border=border)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@app.get("/")
def root():
    return {"service": "qr-code-api", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/qr")
def qr(
    data: str = Query(..., min_length=1, description="Text or URL to encode"),
    format: str = Query("svg", pattern="^(svg|png)$"),
    size: int = Query(10, ge=1, le=40, description="Module box size"),
    border: int = Query(4, ge=0, le=20, description="Quiet zone in modules"),
):
    if len(data) > 2000:
        raise HTTPException(status_code=400, detail="Data too long (max 2000 chars)")
    try:
        if format == "png":
            body = _make_png(data, size, border)
            return Response(content=body, media_type="image/png")
        body = _make_svg(data, size, border)
        return Response(content=body, media_type="image/svg+xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
