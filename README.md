# 📚 Trabalho Final – Sistemas Distribuídos

Este repositório contém as implementações desenvolvidas para o **Trabalho Final da disciplina de Sistemas Distribuídos** da UTFPR. O objetivo principal foi resolver um problema computacionalmente intensivo de forma **sequencial, paralela** e **distribuída**, avaliando o desempenho de cada abordagem.

## 🧠 Problema Escolhido

**Problema do Caixeiro Viajante (TSP)**  
O problema consiste em encontrar o menor caminho possível que permita a um vendedor passar por todas as cidades exatamente uma vez e retornar à cidade de origem.

## 🛠️ Tecnologias Utilizadas

- Linguagem: **Python 3.13**
- Paralelismo: `multiprocessing` (Threads/processos)
- Comunicação distribuída: `socket`
- Ambiente: Windows 10
- IDE: VS Code / Terminal

## 📁 Estrutura do Projeto


## 🚀 Como Executar

### Clonar o repositório

```bash
git clone https://github.com/BrenoRLobo/Trabalho-Final---Sistemas-Distribuidos.git
cd Trabalho-Final---Sistemas-Distribuidos
```

### Executar Sequencial

```bash
cd Sequencial
python tsp_sequencial.py
```

### Executar Paralelo

```bash
cd Paralelo
python tsp_paralelo.py
```

### Executar Distribuído

```bash
cd Distribuido
python server.py

cd Distribuido
python client.py


