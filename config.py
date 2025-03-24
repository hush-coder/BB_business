import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///business.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_INVITE_CODE = os.environ.get('ADMIN_INVITE_CODE') or 'admin123'  # 管理员邀请码
    PERMANENT_SESSION_LIFETIME = timedelta(days=7) 