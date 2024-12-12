# Simulador de Experiências NASA

## Descrição do Projeto

Este projeto é uma simulação multithread de um sistema de gerenciamento de atrações em um ambiente de experiências da NASA, modelando o fluxo de visitantes, tempos de espera e ocupação das atrações.

## Pré-requisitos

- Python 3.x
- Biblioteca padrão de threading
- Biblioteca padrão de queue

## Uso

### Sintaxe de Execução

```bash
python3 nasa.py <N_ATRACOES> <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>
```

### Parâmetros

1. `N_ATRACOES`: Número de atrações diferentes
2. `N_PESSOAS`: Número total de pessoas na simulação
3. `N_VAGAS`: Número máximo de pessoas por atração
4. `PERMANENCIA`: Tempo de permanência em cada atração
5. `MAX_INTERVALO`: Intervalo máximo entre chegadas de pessoas
6. `SEMENTE`: Semente para geração de números aleatórios
7. `UNID_TEMPO`: Unidade de tempo em milissegundos

### Exemplo de Execução

```bash
python3 nasa.py 2 10 5 3 10 42 1000
```

## Funcionalidades

- Geração de visitantes em intervalos aleatórios
- Distribuição de visitantes entre múltiplas atrações
- Controle de ocupação máxima por atração
- Cálculo de tempos médios de espera
- Cálculo da taxa de ocupação

## Saída da Simulação

A simulação produz um relatório que inclui:
- Tempo médio de espera por atração (em milissegundos)
- Taxa de ocupação das atrações

## Modelagem do Sistema

### Threads

- **Gerador de Pessoas**: Cria visitantes e os coloca na fila
- **Gestor de Atração**: Gerencia a fila e libera acesso às atrações
- **Experiência de Pessoa**: Simula o tempo de permanência de cada visitante

### Sincronização

- Utiliza `threading.Lock()` para acesso seguro a recursos compartilhados
- Usa `queue.Queue()` para gerenciamento da fila de visitantes de maneira segura para threads