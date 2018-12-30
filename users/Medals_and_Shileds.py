
#test = 
#{
#    'Astúcia':{'If´s concatenados', 'switch com default', 'tirou um while para por um if'},
#    'Audácia':{'for infinito', 'while infinito', 'lista indexada', 'ponteiro para '}

#    }
#given when a set of badges are received
existing_medals = {'medals':[
    (0,'Comentador'),
    (1,'Resposta'),
    (2,'Valoroso'),
    ],
    'files':[
        (0,'medal-comentador.png'),
        (1,'medal-response.png'),
        (2,'medal-valor.png')
        ]
    }
#given when accomplished some task
existing_badges = {'badges':[
    (0,'Fez um comentário'),
    (1,'Recomendou uma mudança'),
    (2,'Escreveu um desejo'),
    (3,'Compartilhou nas redes sociais'),
    (4,'Respondeu à um comentário'),
    ],
    'relation':[ # (badge, medals, number of badges) 
        (0,0,5),
        (1,1,5),
        (2,1,1),
        (3,2,5),
        (4,2,3),
       ],
    'files':[
        (0,'badge-comment.png'),
        (1,'badge-reply.png'),
        (2,'badge-change.png'),
        (3,'badge-desire.png'),
        (4,'badge-SocialMedia.png'),
        ]
    }

#given when a set of conquests are received
existing_shields = [
    (0,'Astúcia'),
    (1,'Audácia'),
    (2,'Perseverança'),
    ]

#users receive this when they do something to themselves
existing_conquests = {'conquests':[
    (0,'Assista Isso!'),
    (1,'Trouxe alguém'),
    (2,'Respondeu à pesquisa'),
    (3,'Fez um elogio'),
    (4,'Reclamação'),
    (5,'Postagem'),
    ],'relation':[
        (0,2,5),
        (1,2,2),
        (2,0,1),
        (3,1,5),
        (4,1,3),
        (5,0,3),
        ]}