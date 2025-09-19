# Правила

## DDD

```Text
Presentation -> Application -> Domain
                   ↕
             Infrastructure  
```

- `Application` знает про `Domain`
- `Presentation` обращается только к `Application`
- `Infrastructure` реализует контракты/интерфейсы. Знает про ORM/OpenVPN
- `Domain` не знает ни о чём внешнем 