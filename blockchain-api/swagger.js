const swaggerAutogen = require('swagger-autogen')({ openapi: '3.0.0' });

const doc = {
    info: {
        version: "1.0.0",
        title: "Blockchain API",
        description: "This is the blockchain-api service documentation."
    },
    servers: [
        {
            url: 'http://localhost:3000'
        }
    ],
    tags: [
        {
            "name": "Code Request Review",
            "description": "Endpoints"
        },
        {
            "name": "Node User Management",
            "description": "Endpoints"
        },
        {
            "name": "Data Operation Rule",
            "description": "Endpoints"
        },
        {
            "name": "Datasets",
            "description": "Endpoints"
        },
        {
            "name": "Auditing",
            "description": "Endpoints"
        }
    ],
    components: {
        schemas: {
            listOperation: {
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f"
            },
            accessSpecificOperation: {
                $accessId: "e8de5054a3ab4990a18d42a6b014335d",
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f"
            },
            accessSpecificUpdateOperation: {
                $accessId: "e8de5054a3ab4990a18d42a6b014335d",
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f",
                $status: {
                    '@enum': [
                        "granted",
                        "rejected",
                        "revoked"
                    ]
                }
            },
            dataOpSpecificOperation: {
                $dataOpId: "e8de5054a3ab4990a18d42a6b014335d",
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f"
            },
            dataOpSpecificUpdateOperation: {
                $dataOpId: "e8de5054a3ab4990a18d42a6b014335d",
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f",
                $status: {
                    '@enum': [
                        "granted",
                        "rejected",
                        "revoked"
                    ]
                }
            },
            datasetSpecificOperation: {
                $datasetId: "e8de5054a3ab4990a18d42a6b014335d",
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f"
            },
            userSpecificOperation: {
                $accessId: "e8de5054a3ab4990a18d42a6b014335d",
                $dataCustodianId: "info@openmined.org",
                $nodeId: "28d2428661e84555abcda20764aa6c8f"
            }
        },
        securitySchemes:{
            bearerAuth: {
                type: 'http',
                scheme: 'bearer'
            }
        }
    }
};

const outputFile = './swagger-output.json';
const endpointsFiles = ['./webapi.js'];

swaggerAutogen(outputFile, endpointsFiles, doc).then(() => {
    require('./webapi');           // Your project's root file
});