#!/usr/bin/env bash
# Genial Labs · MIND MESTRE — instalação em 1 comando (Linux/macOS/WSL/Git Bash).
# Clona o repositório para ~/.genial-mind-mestre e cria o wrapper ~/.local/bin/mindmestre.
set -euo pipefail

REPO_ZIP="https://codeload.github.com/geniallabsai/mind_mestre/zip/refs/heads/main"
REPO_GIT="https://github.com/geniallabsai/mind_mestre.git"
DEST="$HOME/.genial-mind-mestre"
BIN="$HOME/.local/bin"
NOME_INSTALADO="genial-mind-mestre"

echo "╔══════════════════════════════════════════════════════╗"
echo "║  Genial Labs · MIND MESTRE                            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "[1/4] verificando pré-requisitos…"
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "  python3 não encontrado no PATH. Instale Python 3.7+ e rode de novo." >&2
  exit 1
fi
echo "  $PY ok"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
if [ -d "$DEST" ]; then
  echo "[2/4] repositório já em $DEST — atualizando…"; rm -rf "$DEST"
else
  echo "[2/4] baixando o MindMestre…"
fi
if git clone --depth 1 "$REPO_GIT" "$DEST" >/dev/null 2>&1; then
  echo "  clone git ok"
else
  curl -fsSL "$REPO_ZIP" -o "$TMP/inst.zip" && unzip -q "$TMP/inst.zip" -d "$TMP"
  mv "$TMP"/mind_mestre-* "$DEST" || cp -r "$TMP"/mind_mestre-* "$DEST"
  echo "  zip codeload ok (git indisponível?)"
fi
# normaliza quebras de linha (zip pode trazer CRLF)
find "$DEST" -type f \( -name "*.py" -o -name "*.sh" -o -name "mindmestre" \) -exec sed -i 's/\r$//' {} +

echo "[3/4] criando o comando global…"
mkdir -p "$BIN"
cat > "$BIN/mindmestre" <<'WRAPPER'
#!/bin/sh
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
PY="$(command -v python3 || command -v python)"
[ -z "$PY" ] && { echo 'mindmestre: python3 nao encontrado' >&2; exit 127; }
exec "$PY" "$HOME/.genial-mind-mestre/mindmestre" "$@"
WRAPPER
chmod +x "$BIN/mindmestre"

echo "[4/4] auto-teste…"
if "$BIN/mindmestre" status >/dev/null 2>&1; then
  echo ""
  echo "✓ Genial Labs · MIND MESTRE instalado."
  echo ""
  echo "  próximos passos:"
  echo "    mindmestre                ← banner + menu"
  echo "    mindmestre plano .        ← este diretório vira investigação + plano (PDF+DOCX+Obsidian)"
  echo "    mindmestre conversa .     ← interrogatório socrático calibrado pela sua nuance"
  echo "    mindmestre debate "seu tema""
  case ":$PATH:" in
    *":$BIN:"*) ;;
    *) echo ""
         echo "  avise: adicione $BIN ao PATH  →  export PATH="$BIN:\\$PATH"" ;;
  esac
else
  echo "auto-teste falhou — rode manualmente: $BIN/mindmestre status" >&2
  exit 1
fi
