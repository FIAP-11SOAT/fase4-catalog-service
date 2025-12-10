"""Testes para o módulo de database."""
import os
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import (
    _build_database_url_from_env,
    DATABASE_URL,
    engine,
    SessionLocal,
    Base,
    get_db
)


class TestDatabaseURLBuilder:
    """Testes para a construção da URL do banco de dados."""
    
    def test_db_url_builder_defaults(self):
        """Teste com valores padrão."""
        # Limpa todas as variáveis de ambiente
        env_vars = [
            "DB_USER", "POSTGRES_USER", "DB_PASS", "POSTGRES_PASSWORD",
            "DB_HOST", "DB", "DB_PORT", "POSTGRES_PORT", "DB_NAME", "POSTGRES_DB",
            "DATABASE_URL"
        ]
        
        for k in env_vars:
            os.environ.pop(k, None)
        
        url = _build_database_url_from_env()
        assert url == "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    
    def test_db_url_builder_with_db_prefix(self):
        """Teste com variáveis de ambiente com prefixo DB_."""
        # Limpa variáveis de ambiente
        env_vars = [
            "DB_USER", "POSTGRES_USER", "DB_PASS", "POSTGRES_PASSWORD",
            "DB_HOST", "DB", "DB_PORT", "POSTGRES_PORT", "DB_NAME", "POSTGRES_DB",
            "DATABASE_URL"
        ]
        
        for k in env_vars:
            os.environ.pop(k, None)
        
        # Define variáveis com prefixo DB_
        os.environ["DB_USER"] = "testuser"
        os.environ["DB_PASS"] = "testpass"
        os.environ["DB_HOST"] = "testhost"
        os.environ["DB_PORT"] = "1234"
        os.environ["DB_NAME"] = "testdb"
        
        try:
            url = _build_database_url_from_env()
            assert url == "postgresql+psycopg2://testuser:testpass@testhost:1234/testdb"
        finally:
            # Cleanup
            for k in ["DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]:
                os.environ.pop(k, None)
    
    def test_db_url_builder_with_postgres_prefix(self):
        """Teste com variáveis de ambiente com prefixo POSTGRES_."""
        # Limpa variáveis de ambiente
        env_vars = [
            "DB_USER", "POSTGRES_USER", "DB_PASS", "POSTGRES_PASSWORD",
            "DB_HOST", "DB", "DB_PORT", "POSTGRES_PORT", "DB_NAME", "POSTGRES_DB",
            "DATABASE_URL"
        ]
        
        for k in env_vars:
            os.environ.pop(k, None)
        
        # Define variáveis com prefixo POSTGRES_
        os.environ["POSTGRES_USER"] = "pguser"
        os.environ["POSTGRES_PASSWORD"] = "pgpass"
        os.environ["POSTGRES_PORT"] = "5433"
        os.environ["POSTGRES_DB"] = "pgdb"
        os.environ["DB"] = "pghost"  # DB_HOST alternativo
        
        try:
            url = _build_database_url_from_env()
            assert url == "postgresql+psycopg2://pguser:pgpass@pghost:5433/pgdb"
        finally:
            # Cleanup
            for k in ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_PORT", "POSTGRES_DB", "DB"]:
                os.environ.pop(k, None)
    
    def test_db_url_builder_mixed_env_vars(self):
        """Teste com mistura de variáveis de ambiente (DB_ tem prioridade)."""
        # Limpa variáveis de ambiente
        env_vars = [
            "DB_USER", "POSTGRES_USER", "DB_PASS", "POSTGRES_PASSWORD",
            "DB_HOST", "DB", "DB_PORT", "POSTGRES_PORT", "DB_NAME", "POSTGRES_DB",
            "DATABASE_URL"
        ]
        
        for k in env_vars:
            os.environ.pop(k, None)
        
        # Define ambos os tipos (DB_ deve ter prioridade)
        os.environ["DB_USER"] = "dbuser"
        os.environ["POSTGRES_USER"] = "pguser"
        os.environ["DB_PASS"] = "dbpass"
        os.environ["POSTGRES_PASSWORD"] = "pgpass"
        
        try:
            url = _build_database_url_from_env()
            # DB_ deve ter prioridade
            assert "dbuser:dbpass" in url
            assert "pguser:pgpass" not in url
        finally:
            # Cleanup
            for k in ["DB_USER", "POSTGRES_USER", "DB_PASS", "POSTGRES_PASSWORD"]:
                os.environ.pop(k, None)


class TestDatabaseConfiguration:
    """Testes para a configuração do banco de dados."""
    
    def test_database_url_configuration(self):
        """Teste de configuração da URL do banco."""
        # DATABASE_URL deve estar configurado
        assert DATABASE_URL is not None
        assert isinstance(DATABASE_URL, str)
    
    def test_engine_configuration(self):
        """Teste de configuração do engine SQLAlchemy."""
        assert engine is not None
        # Verifica se pool_pre_ping está configurado
        assert engine.pool._pre_ping is True
    
    def test_session_local_configuration(self):
        """Teste de configuração do SessionLocal."""
        assert SessionLocal is not None
        # SessionLocal é uma instância de sessionmaker, não uma classe
        assert callable(SessionLocal)  # Deve ser callable para criar sessões
    
    def test_base_configuration(self):
        """Teste de configuração da Base."""
        assert Base is not None
        assert hasattr(Base, 'metadata')


class TestGetDbDependency:
    """Testes para a dependência get_db."""
    
    def test_get_db_generator(self):
        """Teste se get_db é um generator."""
        db_gen = get_db()
        assert hasattr(db_gen, '__next__')
        
        # Consome o generator para testá-lo
        try:
            db_session = next(db_gen)
            assert db_session is not None
            # Força o cleanup
            next(db_gen)
        except StopIteration:
            # Comportamento esperado ao final do generator
            pass
    
    @patch('app.db.SessionLocal')
    def test_get_db_closes_session(self, mock_session_local):
        """Teste se get_db fecha a sessão corretamente."""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        db_gen = get_db()
        
        # Consome o generator
        try:
            db_session = next(db_gen)
            assert db_session == mock_session
            
            # Força o cleanup
            next(db_gen)
        except StopIteration:
            pass
        
        # Verifica se close foi chamado
        mock_session.close.assert_called_once()
    
    @patch('app.db.SessionLocal')
    def test_get_db_closes_session_on_exception(self, mock_session_local):
        """Teste se get_db fecha a sessão mesmo em caso de exceção."""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        db_gen = get_db()
        
        try:
            db_session = next(db_gen)
            assert db_session == mock_session
            
            # Simula uma exceção
            db_gen.throw(Exception("Test exception"))
        except Exception:
            pass
        
        # Verifica se close foi chamado mesmo com exceção
        mock_session.close.assert_called_once()


class TestEnvironmentVariablePrecedence:
    """Testes para precedência de variáveis de ambiente."""
    
    def test_database_url_precedence(self):
        """Teste se DATABASE_URL tem precedência sobre outras variáveis."""
        # Salva estado atual
        original_url = os.environ.get("DATABASE_URL")
        
        try:
            # Define DATABASE_URL diretamente
            test_url = "postgresql://direct:url@test:1234/direct"
            os.environ["DATABASE_URL"] = test_url
            
            # Define outras variáveis que não devem ser usadas
            os.environ["DB_USER"] = "ignored"
            os.environ["DB_PASS"] = "ignored"
            
            # Reimporta o módulo para pegar a nova configuração
            import importlib
            import app.db
            importlib.reload(app.db)
            
            assert app.db.DATABASE_URL == test_url
            
        finally:
            # Restaura estado original
            if original_url:
                os.environ["DATABASE_URL"] = original_url
            else:
                os.environ.pop("DATABASE_URL", None)
            
            # Cleanup
            os.environ.pop("DB_USER", None)
            os.environ.pop("DB_PASS", None)
            
            # Reimporta para restaurar configuração original
            import importlib
            import app.db
            importlib.reload(app.db)
