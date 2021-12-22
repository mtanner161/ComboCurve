ComboCurve/WolfePak and Hubspot Integration Tool

This respository covers 3 different data processing needs in order to create Executive dashboard with Operations, Finance and Marketing integrated together. Current plan is to create a lite web application (views.kingoperating.com) which has a SSO login and kicks to a landing page where a PowerBi dashboard will generate. I am breaking this into two parts - building the dashboard and the data warehouse that feeds it and then building the web application. We can deploy the PowerBi dashboard link ASAP, but eventually want a more customized and robusting reporting application for King Operating.

v1.0 - ComboCurve restAPI connection for Econ One Liners and Res Cat Monthly Cash Flow - COMPLETED 12/22/2021
v1.1 - WolfePak .csv processing and cleaning - In Process
v1.2 - Deploy PowerBi internally with Rex - In Process
v1.2 - Hubspot .csv data processing and cleaning - Not Started

v1 dumps a clean, formatted CSV that can be linked to PowerBi for easy refresh once each script has run. Verison 2 will include two specific upgrades. (1) move all data to a central data warehouse - most likely s3 (3 different buckets) and then building a lite-web application
