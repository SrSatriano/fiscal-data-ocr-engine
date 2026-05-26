# Resiliência OCR

## Score de confiança

Por campo: `confidence = min(engine_scores) * validation_multiplier`

## Retry policy

- 3 tentativas com preprocessamentos diferentes
- Após falha → fila manual

## Logs

Nunca logar conteúdo fiscal completo em produção — apenas `document_id` e scores.
