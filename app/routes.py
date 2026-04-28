from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
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

class Mesaj(BaseModel):
    rol: str
    icerik: str

class SohbetIstegi(BaseModel):
    mesaj: str
    profil: IsletmeProfil
    gecmis: Optional[List[Mesaj]] = []

@router.post("/sohbet")
def sohbet(istek: SohbetIstegi):
    sistem_promptu = f"""Sen via.ai'nin yapay zeka sosyal medya asistanısın.

Kullanıcının işletme bilgileri:
- İşletme adı: {istek.profil.isletme_adi}
- Sektör: {istek.profil.sektor}
- Şehir: {istek.profil.sehir}
- Hedef: {istek.profil.hedef}

Görevin:
- Bu işletmeye özel sosyal medya içerikleri üret
- Instagram, TikTok, Facebook için içerik planları yap
- Caption, hashtag, reels fikirleri, kampanya metinleri oluştur
- İşletmenin sektörüne ve hedefine göre strateji öner
- Türkçe yanıt ver
- Kısa, net ve uygulanabilir öneriler sun
- Emoji kullan, samimi ol
- Asla işletme bilgileri dışında konulara girme"""

    mesajlar = []
    for m in istek.gecmis:
        rol = "user" if m.rol == "kullanici" else "assistant"
        mesajlar.append({"role": rol, "content": m.icerik})
    
    mesajlar.append({"role": "user", "content": istek.mesaj})

    yanit = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        system=sistem_promptu,
        messages=mesajlar
    )

    return {"cevap": yanit.content[0].text}