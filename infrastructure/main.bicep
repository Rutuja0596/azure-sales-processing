param location string = 'eastus'
param storageAccountName string = 'salesstorage${uniqueString(resourceGroup().id)}'
param dataFactoryName string = 'salesadf${uniqueString(resourceGroup().id)}'
param functionAppName string = 'salesfunc${uniqueString(resourceGroup().id)}'
param logicAppName string = 'saleslogic${uniqueString(resourceGroup().id)}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
  }
}

resource salesContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${storageAccount.name}/default/sales-files'
  properties: {
    publicAccess: 'None'
  }
}

resource successContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${storageAccount.name}/default/success'
  properties: {
    publicAccess: 'None'
  }
}

resource failedContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${storageAccount.name}/default/failed'
  properties: {
    publicAccess: 'None'
  }
}

resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: dataFactoryName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    repoConfiguration: {
      type: 'FactoryVSTSConfiguration'
      accountName: 'GitHub'
      repositoryName: 'azure-sales-processing'
      collaborationBranch: 'main'
      rootFolder: '/'
    }
  }
}

resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: resourceId('Microsoft.Web/serverfarms', 'consumption-plan')
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
      ]
    }
  }
}

resource logicApp 'Microsoft.Logic/workflows@2019-05-01' = {
  name: logicAppName
  location: location
  properties: {
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      actions: {}
      contentVersion: '1.0.0.0'
      outputs: {}
      parameters: {}
      triggers: {
        manual: {
          type: 'Request'
          kind: 'Http'
        }
      }
    }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'sales-insights-${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

output storageAccountName string = storageAccount.name
output dataFactoryName string = dataFactory.name
output functionAppName string = functionApp.name
output logicAppName string = logicApp.name
output appInsightsConnectionString string = appInsights.properties.ConnectionString
