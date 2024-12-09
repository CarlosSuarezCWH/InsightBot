from transformers import MarianMTModel, MarianTokenizer

class Translator:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-en-es"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)
    
    def to_english(self, text):
        return self._translate(text, source_lang="es", target_lang="en")
    
    def to_target(self, text, target_lang="es"):
        return self._translate(text, source_lang="en", target_lang=target_lang)
    
    def _translate(self, text, source_lang, target_lang):
        batch = self.tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
        translation = self.model.generate(**batch)
        return self.tokenizer.decode(translation[0], skip_special_tokens=True)
