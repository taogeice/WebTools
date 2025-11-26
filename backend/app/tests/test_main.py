"""
主应用测试
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "欢迎使用 WebTools API"}


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
