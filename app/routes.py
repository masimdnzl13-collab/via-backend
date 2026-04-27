from fastapi import APIRouter
from pydantic import BaseModel
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class IsletmeProfil(BaseModel):
    isletme_adi: str
    sektor: str
    sehir: str
    hedef: str

@router.post("/icerik-uret")
def icerik_uret(profil: IsletmeProfil):
    mesaj = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""
Sen küçük işletmeler için sosyal medya uzmanısın.

İşletme bilgileri:
- Ad: {profil.isletme_adi}
- Sektör: {profil.sektor}
- Şehir: {profil.sehir}
- Hedef: {profil.hedef}

Bu işletme için bu hafta 7 günlük sosyal medya içerik planı oluştur.
Her gün için:
1. İçerik fikri
2. Caption (Türkçe)
3. 5 hashtag

Sade ve uygulanabilir olsun.
"""
            }
        ]
    )
    return {"plan": mesaj.content[0].text}