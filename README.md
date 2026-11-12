# EctoLaser

**Pesquisa e desenvolvimento de um sistema de visão computacional para identificar aglomerados de larvas de carrapatos em pastagens**, com instalação futura em equipamento acoplado a um trator.

> **Estado:** projeto em estruturação. Ainda não existe modelo treinado/validado no campo, nem dispositivo de eliminação operacional. O MVP Python v0.1 foi preparado e testado separadamente; a migração de seu código para este repositório está pendente.

## Referências oficiais

- **Código-fonte e documentação técnica (canônico):** https://github.com/TSWill03/EctoLaser
- **Dataset e anotações (Roboflow):** https://app.roboflow.com/wicolly-wicolly03-alcantara/ectolaser/
- **Decisões, pesquisa e continuidade (Notion):** https://app.notion.com/p/416106461b4d81d6aa86db76bb66ecbd

O projeto anteriormente usava o nome temporário **MataCarrapato 2000**. O nome oficial é **EctoLaser**.

## Objetivo

Identificar **aglomerados de larvas de carrapatos nas pontas do capim** (fase de espera do hospedeiro, ou *questing*) durante o deslocamento de um trator. A identificação da espécie necessita de confirmação por especialista; não é seguro supor que todo aglomerado avermelhado nas folhas seja carrapato.

## Arquitetura proposta

```text
Câmeras próximas ao capim
          ↓
OpenCV / modelo YOLO treinado para os dados reais
          ↓
Detecção + rastreamento temporal de aglomerados
          ↓
Filtragem de falsos positivos (sementes, flores etc.)
          ↓
Registro e mapeamento de focos na pastagem
          ↓
Estudo de mecanismo físico seguro (ainda não implementado)
```

## Prioridades

1. Consolidar datasets públicos e criar anotações próprias de larvas **agrupadas sobre capim** no Roboflow do projeto.
2. Separar amostras de treino, validação e teste por talhão/data/sessão, evitando vazamento entre frames consecutivos.
3. Treinar detector experimental e medir recall, precisão, falsos positivos, latência, FPS e robustez a movimentação/vibração do trator.
4. Validar captura óptica real antes de estudar mecanismos de intervenção.
5. Avaliar alternativas de captura/aspiração confinada e biossegurança, sem assumir que laser é solução adequada.

## Limites de segurança

**Nenhum sistema de laser ou outro atuador está autorizado por detecções de IA.** Lasers em capim vivo ou seco apresentam riscos graves de incêndio, reflexos e lesões oculares em pessoas e animais. Não conectar controle de disparo autônomo ao protótipo. A fase inicial é de **monitoramento apenas**.

## Fontes técnicas

- [Autonomous-laser-weed-removal](https://github.com/RishiKrishnah/Autonomous-laser-weed-removal) — arquitetura de detecção, revisão e bloqueio de segurança.
- [Project-Cyclops](https://github.com/rahularepaka/Project-Cyclops) — inspeção por visão computacional aplicada à agricultura.
- [Laser_control](https://github.com/Ildaron/Laser_control) — estudo de visão de pragas e sistemas ópticos.
- [Helios](https://github.com/vrenzd/helios) — processamento edge com OpenCV/YOLO.
- [Carrapatos em diferentes estágios (Roboflow Universe)](https://universe.roboflow.com/ric-workspace/tick-and-flea-detection).

**Fonte canônica dos datasets próprios:** projeto Roboflow indicado acima. Não versionar imagens, pesos, tokens ou API keys sem revisar autorização, privacidade e licença.

## Demonstração com webcam e Arduino UNO (branch de protótipo)

Na branch `feat/uno-vision-prototype`, consulte [Guia de webcam](docs/WEBCAM_DEMO.md) e [Arquitetura UNO + host](docs/ARCHITECTURE.md).

- `demo/webcam_demo.py`: detecta **presença de rosto**, sem reconhecer identidades; lê um QR de demonstração rotulado “Wicolly”.
- `demo/INICIAR_ECTOLASER.bat`: iniciador no Windows com ambiente virtual isolado e OpenCV 4.13.
- `demo/requirements-demo.txt`: dependências da demonstração local.
- `firmware/uno_ectolaser_status/`: LED integrado como indicador opcional, **nunca** disparo de laser.
- Testes automáticos no GitHub Actions (sem câmera, imagens pessoais ou hardware); a webcam real exige execução interativa no computador do usuário.

**Atenção:** ler um crachá QR não autentica a pessoa e detectar uma face não identifica “Wicolly”. Fotografias do Instagram não foram utilizadas. Para o objetivo real do EctoLaser, será necessário um modelo treinado com aglomerados larvais no capim.
