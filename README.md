# Projeto Cloud 
Este projeto consiste em construir uma arquitetura de solução através de scriptis que automatizam todo o processo de criação na aws.

# Como Utilizar

Como primeira etapa clone este repositorio, é necessario instalar as dependencias para executar os scripts desse projeto, para tal execute o seguinte comando:

```
chmod 400 install_load.sh
./install_load.sh
```

Em seguida execute o comando aws configure, para linkar os comandos da maquina à sua conta da aws, informando obrigatoriamente sua Access key ID, Secret access key e region, as outras informações requisitadas durante esse processo são opcionais.
```
aws configure
```

Crie um par de chaves, a public key sera utilizada para configurar as suas instancias, e a private key pode ser usada para acessá-las (Não divulgue essas chaves), essa tarefa pode ser realizada executando o seguinte comando:

```
ssh-keygen -t rsa
```
Por default as chaves serão salvas no diretorio /home/.ssh/, que é uma pasta oculta, depois de criar o par de chaves deve-se executar o comando chmod 400 para estas.

Posteriormente deve-se rodar o script instalador.py, este é responsável por configurar todas os componentes necessários para o funcionamento da sua arquitetura como :

Importação da key pair

Criação do Security Group

Inicialização de uma instancia, que utiliza os componentes anteriores, responsável por executar o load balancer.

Apos executar o script instalador.py deve-se acessar essa instancia manualmente via ssh com sua private key, que foi utilizada no processo de criação da public key, uma vez dentro da instancia, deve-se executar os commandos como root, execute o comando aws configure

Em seguida deve-se acessar a pasta com os scripts que são clonados na inicialização da instancia, para isso pode-se executar os seguintes comandos:

```
cd /
cd / Cloud-Projeto
python3 load.py
```

O arquivo load.py executa o load-balancer, assim como no instalador deve-se informar as informações requisitadas ao executar o script.

# Requisições Api-Rest
Para realizar uma requisição deve-se executar o script tarefas.py, da seguinte forma:

Adicionar Tarefa: (Seta a tarefa existente) - o aplicativo possui apenas uma tarefa que eé alterada com "adicionar"

```
python3 tarefas.py "tarefa adicionar" "$nome" "$descrição" 
```

Listar Tarefa: (Lista a tarefa)

```
python3 tarefas.py "tarefa listar" 
```

E em seguida informar o public ip da intstancia que roda o load-balancer

Os dados são armazenados em um firebase, para alterar o database dessa plataforma deve-se modificar a variavel config no arquivo app.py com suas informações.

Para acessar sua web page via navegador pode-se utilizar : 

```
https://($public_ip):5000/Tarefas/
```
