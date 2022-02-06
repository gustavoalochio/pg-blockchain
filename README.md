# pg-blockchain

- Check to start the development


Start docker-compose chainlink
Start docker-compose 5gempower
Start Adapter 
Check if aws is online
Check if aws docker is up


webhook


type = "webhook"
schemaVersion = 1
name = "eteste"
externalJobID = "089b070a-4bfa-4f3d-9b4f-43c5dd4780d6"
observationSource = """
my_json_task [type="jsonparse"
              data="$(jobRun.requestBody)"
              path="id"]
     my_bridge_task [type="bridge"
                name="bridge-adpter"
                requestData="{\\"id\\": 0,\\"data\\":{\\"id\\": $(my_json_task)}}"
                ]
    my_json_task -> my_bridge_task
"""

subir apenas adapter e chainlink para test 5g ja esta on


  function requestEthereumPrice(address _oracle, string memory _jobId)
    public
    onlyOwner
  {
    Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillEthereumPrice.selector);
    req.add("id", "{\"id\": 0,\"data\":{\"id\": \"00:0D:B9:2F:56:72\"}}");
    req.addInt("times", 100);
    sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
  }