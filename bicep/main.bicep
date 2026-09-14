targetScope = 'resourceGroup'

@description('Azure region for the resources')
param location string = 'australiaeast'

@description('Name of the Azure Container Registry')
param acrName string = 'actuarialaiacr'

@description('Name of the App Service Plan')
param appServicePlanName string = 'actuarial-ai-plan'

@description('Name of the Web App')
param appName string = 'actuarial-ai-app'

@description('Container image to run')
param containerImage string = 'actuarialaiacr.azurecr.io/actuarial-ai:v3'

@description('Name of the Azure SQL logical server')
param sqlServerName string = 'actuarial-ai-sql'

@description('Name of the Azure SQL database')
param sqlDatabaseName string = 'actuarial'

@description('Administrator username for Azure SQL')
param sqlAdminUsername string = 'actuarialadmin'

@description('Administrator password for Azure SQL')
@secure()
param sqlAdminPassword string

module acr 'acr.bicep' = {
  name: 'acrDeployment'
  params: {
    acrName: acrName
    location: location
  }
}

module appServicePlan 'appservice-plan.bicep' = {
  name: 'appServicePlanDeployment'
  params: {
    planName: appServicePlanName
    location: location
  }
}

module appService 'appservice.bicep' = {
  name: 'appServiceDeployment'
  params: {
    appName: appName
    appServicePlanName: appServicePlanName
    location: location
    containerImage: containerImage
  }
}

module acrPull 'acr-pull.bicep' = {
  name: 'acrPullDeployment'
  params: {
    acrName: acrName
    principalId: appService.outputs.webAppPrincipalId
  }
}

module sql 'sql.bicep' = {
  name: 'sqlDeployment'
  params: {
    sqlServerName: sqlServerName
    sqlDatabaseName: sqlDatabaseName
    sqlAdminUsername: sqlAdminUsername
    sqlAdminPassword: sqlAdminPassword
    location: location
  }
}

output resourceGroupName string = resourceGroup().name
output resourceGroupLocation string = resourceGroup().location
output containerRegistryName string = acr.outputs.containerRegistryName
output appServicePlanName string = appServicePlan.outputs.appServicePlanName
output appName string = appService.outputs.webAppName
output appPrincipalId string = appService.outputs.webAppPrincipalId
output sqlServerName string = sql.outputs.sqlServerName
output sqlDatabaseName string = sql.outputs.sqlDatabaseName
