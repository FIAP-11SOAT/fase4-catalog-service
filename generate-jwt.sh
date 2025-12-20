#!/usr/bin/env bash
set -e

# ======================================================
# CONFIGURAÇÕES
# ======================================================

PRIVATE_KEY_FILE="./private_key.pem"
KID="local-dev-key"
ISSUER="local-dev"
SUBJECT="local-user"
TTL_SECONDS=3600

# ======================================================
# VALIDACOES
# ======================================================

if [ ! -f "$PRIVATE_KEY_FILE" ]; then
  echo "❌ Arquivo $PRIVATE_KEY_FILE não encontrado"
  exit 1
fi

ROLE="$1"

if [ -z "$ROLE" ]; then
  echo "❌ Uso: ./generate-jwt.sh <ROLE>"
  echo "   Exemplo: ./generate-jwt.sh CUSTOMERS"
  exit 1
fi

# ======================================================
# FUNÇÕES
# ======================================================

b64url() {
  openssl base64 -e -A | tr '+/' '-_' | tr -d '='
}

# ======================================================
# HEADER
# ======================================================

HEADER=$(cat <<EOF
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "$KID"
}
EOF
)

# ======================================================
# PAYLOAD
# ======================================================

NOW=$(date +%s)
EXP=$((NOW + TTL_SECONDS))

PAYLOAD=$(cat <<EOF
{
  "sub": "$SUBJECT",
  "iss": "$ISSUER",
  "iat": $NOW,
  "exp": $EXP,
  "user_type": "$ROLE"
}
EOF
)

# ======================================================
# ASSINATURA
# ======================================================

JWT_HEADER=$(echo -n "$HEADER" | b64url)
JWT_PAYLOAD=$(echo -n "$PAYLOAD" | b64url)

SIGNING_INPUT="$JWT_HEADER.$JWT_PAYLOAD"

SIGNATURE=$(echo -n "$SIGNING_INPUT" \
  | openssl dgst -sha256 -sign "$PRIVATE_KEY_FILE" \
  | b64url)

JWT="$SIGNING_INPUT.$SIGNATURE"

# ======================================================
# OUTPUT
# ======================================================

echo ""
echo "✅ JWT gerado com sucesso"
echo ""
echo "$JWT"
echo ""
