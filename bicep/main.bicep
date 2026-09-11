targetScope = 'subscription'

@description('Name of the resource group for the Actuarial AI application')
param resourceGroupName string = 'actuarial-ai-rg'

@description('Azure region for the resources')
param location string = 'australiaeast'

@description('Name of the Azure Container Registry')
param acrName string = 'actuarialaiacr'

@description('Name of the App Service Plan')
param appServicePlanName string = 'actuarial-ai-plan'

@description('Name of the Web App')
param appName string = 'actuarial-ai-app'
@description('Container image to run')
param containerImage string = 'actuarialaiacr.azurecr.io/actuarial-ai:latest'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: location
  tags: {
    project: 'actuarial-ai'
    environment: 'development'
  }
}

module acr 'acr.bicep' = {
  name: 'acrDeployment'
  scope: resourceGroup
  params: {
    acrName: acrName
    location: location
  }
}

module appServicePlan 'appservice-plan.bicep' = {
  name: 'appServicePlanDeployment'
  scope: resourceGroup
  params: {
    planName: appServicePlanName
    location: location
  }
}
module appService 'appservice.bicep' = {
  name: 'appServiceDeployment'
  scope: resourceGroup
  params: {
    appName: appName
    appServicePlanName: appServicePlanName
    location: location
    containerImage: containerImage
  }
}

module acrPull 'acr-pull.bicep' = {
  name: 'acrPullDeployment'
  scope: resourceGroup
  params: {
    acrName: acrName
    principalId: appService.outputs.webAppPrincipalId
  }
}
output resourceGroupName string = resourceGroup.name
output resourceGroupLocation string = resourceGroup.location
output containerRegistryName string = acr.outputs.containerRegistryName
output appServicePlanName string = appServicePlan.outputs.appServicePlanName
output appName string = appService.outputs.webAppName
output appPrincipalId string = appService.outputs.webAppPrincipalId
