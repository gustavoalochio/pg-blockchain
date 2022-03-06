# pg-blockchain

- Check to start the development


Start docker-compose chainlink
Start docker-compose 5gempower
Start Adapter 
Check if aws is online
Check if aws docker is up

bridge-adapter
http://200.137.66.33:8081



Passo 1:

Na IDE Remix compile e faca o deploy do contrato Operator.sol passando o address do token LINK na rede rinkeby

address LINK token rinkeby: 0x01BE23585060835E02B77ef475b0Cc51aA1e0709

Nesse mesmo contrato utilize o metodo setAuthorizedSenders para autorizar o chainlink node a enviar requests para esse oraculo

senders: ["0x0209b698fc9B5917508629A7Da7d19159eD6D3Aa"]

Passo 2:

Crie um job na dashboard do chainlink node passando o conteudo do arquivo pipeline.toml lembrando de alterar
o contractAddress e o submit_tx com o address do contrato do Operator.sol no passo 1

Apos esse passo salve o jobId gerado

Passo 3:

Na IDE Remix compile e faca deploy do contrato Validator.sol passando o path a ser verificado pelo contrato,
o jobId do passo 2 e o endereco do Operator.sol do passo 1

Apos o deploy, utilize sua carteira do metamask para enviar token's LINK para esse contrato conseguir realizer requisicoes ao Oraculo(Operator.sol)

Passo 4:

Realize uma chamada requestUpdateHash no contrato Validator.sol, sera a primeira vez que o contrato sera preenchido, apos algum tempo, verifique o conteudo
de hashIpfs com o metodo getHash()

Passo 5:

Apos estar preenchido crie um novo job na dashboard do chainink node, passando o conteudo de pipeline-cron.toml, assim sera criado um verificador de tempos em tempos
para checar se o conteudo da api ainda esta valido com a hash do ipfs


Caso o conteudo do path seja alterado um erro sera disparado no job de validacao
Caso nao seja alterado uma mensagem de conteudo valido eh liberada.

