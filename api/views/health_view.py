from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from flask import jsonify

health_tag = Tag(name="Health", description="Verifica o status da API")

health_bp = APIBlueprint(
    'health',
    __name__,
    url_prefix="/",
    abp_tags=[health_tag]
)

@health_bp.get("/health")
def health_check():
    return jsonify(status="ok"), 200