from schemas.resource_schema import ResourceSchema


def format_resource_text(resource: ResourceSchema) -> str:
    formatted_is_checked = "✅ Да" if resource.verified else "❌ Нет"
    formatted_tags = " ".join(f"{t.strip()}" for t in resource.tags.split())
    formatted_created_at = resource.created_at.strftime("%d %B %Y, %H:%M")

    text = f"""
<b>{resource.name}</b>

<i>{resource.description}</i>

{resource.links}

Категория: {resource.category.name}
Проверен: {formatted_is_checked}

Теги: {formatted_tags}

🕒 {formatted_created_at}
"""
    return text
