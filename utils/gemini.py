from google import genai
from google.genai import types
from loader import db

class Geminiutils():

    def __init__(self) -> None:
        self.client = genai.Client(api_key="AIzaSyDCYRBoyDrNEf154YntSmY92XQvthVRO-8")

    def add_chiqim_f(self, summa: int, kategoriya: str, izoh: str):
        result = db.add_chiqim(summa, izoh, kategoriya, 23)
        print("chiqim saqlandi")
        return result


    def add_kirim_f(self, summa: int, kategoriya: str, izoh: str):
        result = db.add_kirim(summa, izoh, kategoriya)
        print("kirim saqlandi")
        return result

    def get_text(self, audio):
        myfile = self.client.files.upload(file=audio)
        prompt = "Ushbu o'zbek tilidagi audioni matnga aylantir"

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, myfile]
        )
        return response.text

    def add_transaction(self, text):
        add_chiqim = {
            "name": "add_chiqim_f",
            "description": "chiqimlarni saqlash uchun",
            "parameters": {
                "type": "object",
                "properties": {
                    "summa": {"type": "integer", "description": "chiqim summasi"},
                    "kategoriya": {
                        "type": "string",
                        "enum": ["ovqat", "kiyim", "mashina", "ta'lim", "boshqa", "yo'q"],
                        "description": "chiqim kategoriyasi agar chiqim kategoriyasi bo'lmasa 'boshqa' ni tanlang",
                    },
                    "izoh": {"type": "string", "description": "qo'shimcha izoh agar izoh bo'lamasa 'yoq' deb yoz"},
                },
                "required": ["summa", "kategoriya", "izoh"],
            },
        }

        add_kirim = {
            "name": "add_kirim_f",
            "description": "kirimlarni saqlash uchun",
            "parameters": {
                "type": "object",
                "properties": {
                    "summa": {"type": "integer", "description": "kirim summasi"},
                    "kategoriya": {
                        "type": "string",
                        "enum": ["ish haqi", "sovg'a", "savdo", "boshqa"],
                        "description": "kirim kategoriyasi agar kirim kategoriyasi bo'lmasa 'boshqa' ni tanlang",
                    },
                    "izoh": {"type": "string", "description": "qo'shimcha izoh agar izoh bo'lamasa 'yoq' ni yozing"},
                },
                "required": ["summa", "kategoriya", "izoh"],
            },
        }

        # Gemini uchun tool’lar
        tool = types.Tool(function_declarations=[add_chiqim, add_kirim])
        contents = [types.Content(role="user", parts=[types.Part(text=text)])]
        config = types.GenerateContentConfig(tools=[tool])

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )

        try:
            tool_call = response.candidates[0].content.parts[0].function_call
        except Exception as e:
            print("Function call yo‘q:", response.text)
            return None

        if tool_call:
            if tool_call.name == "add_chiqim_f":
                return self.add_chiqim_f(**tool_call.args)
            elif tool_call.name == "add_kirim_f":
                return self.add_kirim_f(**tool_call.args)

        print("Model function_call qaytarmadi. Javob:", response.text)
        return None
