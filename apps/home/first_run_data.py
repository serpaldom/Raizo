import os
import csv
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .models import MitreTactic, MitreTechnique, Technologies, Tag

# Obtener el modelo de usuario actual
User = get_user_model()

# Obtener el usuario actual
current_user = User.objects.first()

# Obtener la ruta del archivo CSV relativa a la ubicación actual de views.py
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_directory, "default_data.csv")

# Abrir el archivo CSV
with open(csv_file_path, "r") as file:
    # Crear un lector CSV
    reader = csv.DictReader(file)

    # Crear las tactics
    if "tactics" in reader.fieldnames:
        for row in reader:
            tactic_id = row["ID"]
            tactic_name = row["Name"]

            tactic, _ = MitreTactic.objects.get_or_create(id=tactic_id)
            tactic.name = tactic_name
            tactic.created_by = current_user
            tactic.save()

    # Volver al inicio del archivo CSV
    file.seek(0)

    # Crear las techniques
    if "techniques" in reader.fieldnames:
        for row in reader:
            technique_id = row["ID"]
            technique_name = row["Name"]

            technique, _ = MitreTechnique.objects.get_or_create(id=technique_id)
            technique.name = technique_name
            technique.created_by = current_user
            technique.save()

    # Volver al inicio del archivo CSV
    file.seek(0)

    # Crear las technologies
    if "technologies" in reader.fieldnames:
        for row in reader:
            technology_id = row["ID"]
            technology_name = row["Name"]

            technology, _ = Technologies.objects.get_or_create(id=technology_id)
            technology.name = technology_name
            technology.created_by = current_user
            technology.save()

    # Volver al inicio del archivo CSV
    file.seek(0)

    # Crear las tags
    if "tags" in reader.fieldnames:
        for row in reader:
            tag_id = row["ID"]
            tag_name = row["Name"]

            tag, _ = Tag.objects.get_or_create(id=tag_id)
            tag.name = tag_name
            tag.created_by = current_user
            tag.save()
