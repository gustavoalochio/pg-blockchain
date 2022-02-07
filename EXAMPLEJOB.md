type = "directrequest"
schemaVersion = 1
name = "example eth request event spec"
contractAddress = "0x933727673C306C07b48E7756233D12e1f3e3ce4a"
maxTaskDuration = "0s"
observationSource = """

    decode_log   [type=ethabidecodelog
                  abi="OracleRequest(bytes32 indexed specId, address requester, bytes32 requestId, uint256 payment, address callbackAddr, bytes4 callbackFunctionId, uint256 cancelExpiration, uint256 dataVersion, bytes data)"
                  data="$(jobRun.logData)"
                  topics="$(jobRun.logTopics)"]

    decode_cbor  [type=cborparse data="$(decode_log.data)"]

     my_bridge_task [type="bridge"
                name="bridge-adpter"
                requestData="{\\"id\\":  $(jobSpec.externalJobID),\\"data\\":{\\"id\\": $(decode_cbor.id)}}"
                ]
encode_data  [type="ethabiencode" abi="(bytes32 requestId, bytes data)" 
    data="{ \\"requestId\\": $(decode_log.requestId), \\"data\\": $(my_bridge_task) }"]

    encode_tx    [type=ethabiencode
                  abi="fulfillOracleRequest2(bytes32 requestId, uint256 payment, address callbackAddress, bytes4 callbackFunctionId, uint256 expiration, bytes data)"
                  data="{\\"requestId\\": $(decode_log.requestId), \\"payment\\": $(decode_log.payment), \\"callbackAddress\\": $(decode_log.callbackAddr), \\"callbackFunctionId\\": $(decode_log.callbackFunctionId), \\"expiration\\": $(decode_log.cancelExpiration), \\"data\\": $(encode_data)}"
                 ]

    submit_tx    [type=ethtx to="0x933727673C306C07b48E7756233D12e1f3e3ce4a" data="$(encode_tx)"]

    decode_log -> decode_cbor -> my_bridge_task -> encode_data -> encode_tx -> submit_tx
"""
externalJobID = "db162c51-53b2-4f7c-8eae-1e657ec7e2d1"