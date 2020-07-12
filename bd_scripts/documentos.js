db = db.getMongo().getDB("easypark");

db.usuarios.insert(
  {
    "cpf": "12345678901",
    "acordos": [
      {
        "id_acordo": 1,
        "nota_pm": 4, 
        "nota_mp": 5
      },
      {
        "id_acordo": 2
      }
    ]
  }
);

db.usuarios.insert(
  {
    "cpf": "12345678902",
    "acordos": [
      {
        "id_acordo": 1,
        "nota_pm": 4, 
        "nota_mp": 5
      }
    ]
  }
);

db.usuarios.insert(
  {
    "cpf": "12345678903",
    "acordos": [
      {
        "id_acordo": 2
      }
    ]
  }
);

db.vagas.insert(
  {
    "id_vaga": 1,
    "acordos": [
      {
        "id_acordo": 1,
        "nota_pm": 4, 
        "nota_mp": 5
      },
      {
        "id_acordo": 2
      }
    ],
    "avaliacoes": [
      {
        "cpf_agente": '12345678904',
        "resultado": false,
        "comentario": "Largura inapropriada"
      },
      {
        "cpf_agente": '12345678904',
        "resultado": true
      }
    ]
  }
);

db.vagas.insert(
  {
    "id_vaga": 2,
    "acordos": [],
    "avaliacoes": [
      {
        "cpf_agente": '12345678904',
        "resultado": true
      }
    ]
  }
);

db.vagas.insert(
  {
    "id_vaga": 3,
    "acordos": [],
    "avaliacoes": [
      {
        "cpf_agente": '12345678904',
        "resultado": true
      }
    ]
  }
);
