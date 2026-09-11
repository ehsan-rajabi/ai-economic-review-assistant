targetScope = 'resourceGroup'

@description('Name of the Azure Container Registry')
param acrName string

@description('Azure region for the registry')
param location string

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2025-04-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

output containerRegistryName string = containerRegistry.name
