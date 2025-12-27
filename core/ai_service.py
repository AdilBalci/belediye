import requests
import json
import logging
import os

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def analyze_complaint_text(text):
    """
    Analyzes the complaint text using OpenRouter AI.
    Returns a dictionary with summary, category, and urgency.
    """
    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY is not set.")
        return {
            "summary": "AI Analizi için API Anahtarı girilmedi.",
            "category": "Beklemede",
            "urgency": "Belirsiz",
            "suggested_unit": "Sistem Yöneticisi"
        }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://belediye-sistemi.com", # Required by OpenRouter
        "X-Title": "Belediye Sistemi"
    }

    prompt = f"""
    Aşağıdaki vatandaş şikayetini analiz et.
    Lütfen yanıtı SADECE geçerli bir JSON formatında ver. Başka bir metin ekleme.
    JSON formatı şöyle olmalı:
    {{
        "summary": "Şikayetin kısa özeti (maksimum 1 cümle)",
        "category": "Şikayet kategorisi (Örn: Fen İşleri, Park ve Bahçeler, Zabıta, Temizlik, Ulaşım)",
        "urgency": "Aciliyet durumu (Düşük, Orta, Yüksek)",
        "suggested_unit": "Yönlendirilmesi gereken birim adı"
    }}

    Şikayet Metni:
    "{text}"
    """

    data = {
        "model": "openai/gpt-3.5-turbo", # Cost effective and fast
        "messages": [
            {"role": "system", "content": "Sen bir belediye şikayet analiz uzmanısın. Cevapların her zaman Türkçe ve JSON formatında olmalı."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=10)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        # Clean up code blocks if AI wraps in ```json ... ```
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        return json.loads(content)

    except Exception as e:
        logger.error(f"AI Analysis failed: {e}")
        return {
            "summary": "Analiz sırasında hata oluştu.",
            "category": "Belirsiz",
            "urgency": "Belirsiz",
            "suggested_unit": "Yönetici İncelemesi Gerekiyor"
        }
