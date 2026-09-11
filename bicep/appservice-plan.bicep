targetScope = 'resourceGroup'

@description('Name of the App Service Plan')
param planName string

@description('Azure region for the App Service Plan')
param location string

resource appServicePlan 'Microsoft.Web/serverfarms@2025-03-01' = {
  name: planName
  location: location
  kind: 'linux'
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true
  }
}

output appServicePlanName string = appServicePlan.name
