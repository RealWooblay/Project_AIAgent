const { create, filesFromPaths } = require('@web3-storage/w3up-client');
const fs = require('fs');
require('dotenv').config({ path: '../.env' });

async function storeData(data) {
    const client = await create();
    await client.login(process.env.WEB3_STORAGE_EMAIL);
    const spaceDid = process.env.WEB3_STORAGE_SPACE_DID;
    await client.setCurrentSpace(spaceDid);

    const buffer = Buffer.from(JSON.stringify(data));
    fs.writeFileSync('data.json', buffer);

    const files = await filesFromPaths(['data.json']);
    const cid = await client.uploadDirectory(files);
    return cid;
}

const summaries = process.argv[2];
if (summaries) {
    const parsedSummaries = JSON.parse(summaries);
    storeData(parsedSummaries).then(cid => {
        console.log(`Stored data with CID: ${cid}`);
    }).catch(error => {
        console.error('Error storing data:', error);
    });
} else {
    console.log('Please provide summaries to store');
}

// This needs to store the AI responses on Filecoin using web3.storage