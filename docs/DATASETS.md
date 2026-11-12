# Datasets do EctoLaser

## Roboflow oficial

Projeto de imagens e anotações: https://app.roboflow.com/wicolly-wicolly03-alcantara/ectolaser/

O link foi fornecido pelo responsável do projeto. **O conteúdo privado, o número de imagens, as classes e a versão publicada do Roboflow ainda não foram acessados nem verificados.** Não comitar chave API ou dados brutos sem revisão.

## Bases candidatas para auditoria

| Fonte | Link | Uso proposto |
| --- | --- | --- |
| Tick Citizenscience | https://universe.roboflow.com/tickcitizenscience/tick-qk4y9 | Pré-treinamento de carrapatos, analisar domínio |
| Ticks Image Detection | https://universe.roboflow.com/ticks-gftpi/ticks-image-detection | Detecção geral de carrapatos |
| Tick and Flea Detection | https://universe.roboflow.com/ric-workspace/tick-and-flea-detection | Investigar classe de larvas |
| ITICK (Zenodo) | https://zenodo.org/records/14353933 | Candidata para reconhecimento de espécies/gêneros |
| R. microplus larvae questing (Wikimedia) | https://commons.wikimedia.org/wiki/File:Rhipicephalus-microplus-larvae-questing.jpg | Exemplo visual diretamente próximo da aplicação |
| Plant Species Identification (Zenodo) | https://zenodo.org/records/17741075 | Exemplos negativos de estruturas vegetais |

**Não há comprovação de que as bases de carrapatos adultos sejam suficientes para reconhecer aglomerados de larvas em capim sob movimento de trator.**

## Protocolo proposto

- Classe inicial: `cluster_larvas_pasto`, com anotação de uma caixa por aglomerado.
- Positivos: fotografias e quadros de vídeo de aglomerados larvais nas pontas do capim, com confirmação veterinária/taxonômica.
- Negativos: sementes, flores, fungos, insetos, pequenas folhas, sombras e sujeira.
- Splits: separar por coleta, talhão e data; evitar amostras do mesmo vídeo em treino e teste.
- Métricas: recall e precisão por foco, falsos positivos por área/tempo, mAP, FPS, latência e deslocamento de localização.
- Proveniência: registrar versão do Roboflow, fonte, licença e data de obtenção antes de usar dados de terceiros.

**Nenhuma base acima foi importada ou treinada nesta etapa.**