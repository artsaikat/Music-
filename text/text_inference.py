from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

tokenizer = DistilBertTokenizer.from_pretrained(r"C:\Users\Saikat Maiti\Desktop\Music recommendation\text\saved_model1")
model = DistilBertForSequenceClassification.from_pretrained(r"C:\Users\Saikat Maiti\Desktop\Music recommendation\text\saved_model")

label_map = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
}


def predict_emotion(text):

    model.eval()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64,
    )

    inputs = {
        k: v.to(model.device)
        for k, v in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(
        outputs.logits,
        dim=1
    )

    pred = torch.argmax(
        probs,
        dim=1
    ).item()

    confidence = probs[0][pred].item()

    return label_map[pred], confidence