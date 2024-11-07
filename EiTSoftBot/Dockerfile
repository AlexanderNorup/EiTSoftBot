FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["EiTSoftBot.Dto/", "EiTSoftBot.Dto/"]
COPY EiTSoftBot.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish --no-restore -c Release -o /app 

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080
ENTRYPOINT ["dotnet", "EiTSoftBot.dll"]