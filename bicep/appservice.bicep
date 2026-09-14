targetScope = 'resourceGroup'

@description('Name of the Web App')
param appName string

@description('Name of the existing App Service Plan')
param appServicePlanName string

@description('Azure region for the Web App')
param location string

@description('Container image to run')
param containerImage string

@description('Azure SQL server hostname')
param sqlServer string

@description('Azure SQL database name')
param sqlDatabase string

@description('Azure SQL administrator username')
param sqlUser string

@description('Azure SQL administrator password')
@secure()
param sqlPassword string

resource appServicePlan 'Microsoft.Web/serverfarms@2025-03-01' existing = {
  name: appServicePlanName
}

resource webApp 'Microsoft.Web/sites@2025-03-01' = {
  name: appName
  location: location
  kind: 'app,linux,container'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id

    siteConfig: {
      linuxFxVersion: 'DOCKER|${containerImage}'
      acrUseManagedIdentityCreds: true
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'SQL_SERVER'
          value: sqlServer
        }
        {
          name: 'SQL_DATABASE'
          value: sqlDatabase
        }
        {
          name: 'SQL_USER'
          value: sqlUser
        }
        {
          name: 'SQL_PASSWORD'
          value: sqlPassword
        }
        {
          name: 'SQL_PORT'
          value: '1433'
        }
      ]
    }
  }
}

output webAppName string = webApp.name
output webAppPrincipalId string = webApp.identity.principalId
