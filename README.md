# Viwer3D: Motor e Visualizador 3D (Cirurgic3D)

O **Viwer3D** é o motor de visualização e processamento de imagens médicas da **Cirurgic3D**. Desenvolvido em **Python** e baseado no framework **trame-slicer**, este projeto oferece uma plataforma robusta e **web-native** para visualização 3D, reconstrução multiplanar (**MPR**) e segmentação avançada de dados volumétricos.

---

# 🚀 Visão Geral

O projeto funciona como um intermediário entre poderosas bibliotecas de computação científica (**VTK/Slicer**) e a interface do usuário no navegador. Ele permite que profissionais visualizem exames complexos, realizem marcações e executem segmentações anatômicas com **performance de desktop em um ambiente web**.

---

# 🌐 Deploy Online

Uma instância pública do Viwer3D está disponível para demonstração e testes diretamente no navegador.

Acesse o deploy:

🔗 https://huggingface.co/spaces/Kayrck/viewer3D

Esta versão está hospedada no Hugging Face Spaces, utilizando infraestrutura otimizada para aplicações Python interativas. O ambiente permite visualizar o funcionamento do motor Viwer3D sem necessidade de instalação local.

Principais benefícios do deploy:

Demonstração rápida da plataforma

Ambiente acessível para testes e validação

Distribuição simplificada para apresentações técnicas

Integração com containers e pipelines de deploy

# ✨ Principais Funcionalidades

### Visualização Multimodal
Suporte para visualização **3D** e fatias **2D (Axial, Sagital e Coronal)** simultâneas.

### Segmentação Avançada
Ferramentas integradas para:

- **Paint (Pintura)**
- **Erase (Borracha)**
- **Threshold (Limiarização)**
- Remoção de **"ilhas"**

### Renderização de Volume
Algoritmos otimizados para visualização de:

- Tecidos
- Ossos
- Estruturas vasculares

### Gestão de Markups
Adição e manipulação de **pontos de controle e fidelidade anatômica**.

### Presets Médicos
Configurações pré-definidas de **janelamento (Window/Level)** para **CT e MR**.

### Interface Flexível
Layouts customizáveis baseados em componentes **trame**.

---

# 🛠️ Tecnologias Utilizadas

- **Trame**  
  Framework para criação de aplicações web visuais em Python.

- **VTK/Slicer**  
  Motores de processamento e renderização 3D.

- **Vue.js (via Trame)**  
  Construção da interface reativa.

- **Docker**  
  Garantia de portabilidade e facilidade de deploy (incluindo suporte para **Hugging Face Spaces**).

---

# 📂 Estrutura do Projeto
/trame_slicer
→ O núcleo do motor. Contém a lógica de IO, gerenciamento de visualização,
layouts e ferramentas de segmentação.

/examples
→ Demonstrações de implementação, incluindo:
medical_viewer_app.py
segmentation_app.py

/resources
→ Presets de visualização, ícones e terminologias DICOM. 

---

# ⚙️ Instalação e Configuração

## Pré-requisitos

- **Python 3.10+**
- **Pip**

---

## Instalação local

Clone o repositório:

```bash
git clone https://github.com/[seu-usuario]/viwer3d.git
cd viwer3d
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
(Opcional) Se estiver utilizando o wheel específico para Slicer/VTK incluído:
```bash
pip install vtk_mrml-9.4.0-cp310-cp310-manylinux_2_35_x86_64.whl
```
# 🖥️ Como Executar

Para iniciar o visualizador médico padrão:
```bash
python examples/medical_viewer_app.py
```
Acesse no navegador:
http://localhost:8080

# 🐳 Docker e Deploy

O projeto está pronto para ser containerizado e implantado em serviços como Hugging Face Spaces.

Construir a imagem
```bash
docker-compose build
```
Rodar o container
```bash
docker-compose up
```
# 🎨 Identidade Visual (Cirurgic3D)

Este projeto foi projetado para ser facilmente customizável. As cores e logotipos podem ser ajustados nos componentes de UI em:
```bash
examples/viewer_lib/ui
```

Isso permite aderência total à paleta visual da Cirurgic3D.

Este README serve como guia técnico e comercial para o motor que sustenta a visualização 3D da Cirurgic3D. Para dúvidas ou contribuições, entre em contato com a equipe de desenvolvimento.
