from rest_framework import serializers

links = {"https://", "http://", "www."}

def no_links(value):
    if any(word in value.lower() for word in links):
        raise serializers.ValidationError("Ссылки в объявлениях запрещены.")
