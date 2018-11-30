# Projeto Cloud 
Este projeto coniste em constuir uma arquitetura de solução atravez de scriptis que automatizão todo o processo de criação na aws.

# Como Utilizar

Como primeira etapa deve-se rodar o script instalador.py, este é responsavel por configurar todas os componentes necessarios para o funcionamento das instancias, como :
Importação da key pair
Criação do Security Group
Inicialização de uma instancia, que utiliza os componentes anteriores, responsavel por executar o load balancer.

Apos executar o script instalador.py deve-se acessar essa instancia manualmente via ssh com sua private key que foi utilizada no processo de criação da public key, uma vez dentro da instancia é necessario executar o comando aws configure, para linkar os comandos da maquina a sua conta da aws, informando obrigatoriamente sua Access key ID, Secret access key e region, as outras informações requisitadas durante esse processo são opicionais.

Em seguida deve-se acessar a pasta com os scripts que são clocados na inicialização da intancia, para isso pode-se executar os seguintes comandos:

cd /
cd / Cloud-Projeto
python3 load.py

O arquivo load.py executa o load-balancer, assim como no instalador deve-se informar as informações necessarias ao executar o script.

# Requisições
Para realizar uma requisição deve-se executar o script tarefas.py, da seguinte forma:

Adicionar Tarefa: (Seta a tarefa existente) - o aplicativo possui apenas uma tarefa que e alterada com "adicionar"

python3 tarefas.py "tarefa adicionar" "$nome" "$descrição" 


Listar Tarefa: (Lista a tarefa)

python3 tarefas.py "tarefa listar" 

E em seguida informar o public ip da intstancia que roda o load-balancer

Os dados são armazenados em um firebase, para alterar o database dessa plataforma deve-se modificar a variavel config no arquivo app.py com suas informações.