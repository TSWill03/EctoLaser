# Roadmap — EctoLaser

## Fase 0 — Escopo e infraestrutura (atual)

- Nome oficial: **EctoLaser**; nome anterior de trabalho: MataCarrapato 2000.
- Veículo: **trator** com equipamento acoplado, operação na **pastagem**.
- Alvo visual: **aglomerados larvais** na vegetação, não carrapatos aderidos a animais.
- Recursos canônicos: GitHub `TSWill03/EctoLaser`, Roboflow `wicolly-wicolly03-alcantara/ectolaser`, Notion do projeto.
- O MVP Python v0.1 existe em ZIP da conversa anterior; **ainda não foi migrado para o GitHub**.

## Fase 1 — Detector e base de imagens (pendente)

- Auditar imagens e rótulos dos datasets públicos; coletar imagens representativas de pastagem local.
- Definir classe de aglomerado `cluster_larvas_pasto` e negativos difíceis.
- Treinar YOLO de detecção visual; comparar precisão, recall e falsos positivos em testes de campo.

## Fase 2 — Plataforma óptica (pendente)

- Câmeras próximas do capim, proteção a poeira, vibração, variação da altura da vegetação e iluminação.
- Ensaios em bancada, equipamento parado e baixa velocidade; telemetria e registro de posições dos focos.
- Medir taxa real de detecção e área coberta, sem atuação física.

## Fase 3 — Controle físico (pesquisa, não implementado)

- Comparar métodos de remoção seguros, incluindo aspiração/coleta confinada com manejo apropriado do material.
- Analisar incêndio, reflexos e risco ocular antes de qualquer hipótese envolvendo laser em campo.
- Somente avançar mediante validação independente de segurança e eficácia. Nenhuma detecção de software deve autorizar disparo.

## Fase 4 — Validação (futuro)

- Ensaios controlados com grupos de comparação e apoio veterinário.
- Quantificar larvas coletadas ou focos tratados, efeito no ciclo do carrapato, robustez, manutenção e custo por hectare.

**Estado: fase de P&D.**