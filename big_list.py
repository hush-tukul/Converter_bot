options = {
    'convert':
        {
            'docx': [
                (".pdf", 'pdf'),
                (".txt", 'txt'),
            ],
            'pdf': [
                #(".png", 'png'),
                #(".jpeg", 'jpeg'),
                (".docx", 'docx'),
                #(".txt", 'txt'),
            ],
            'png': [
                (".jpeg", 'jpeg'),
                #(".pdf", 'pdf'),
                #(".docx", 'docx'),
                (".txt", 'txt'),
            ],
            'jpeg': [
                #(".png", 'png'),
                #(".pdf", 'pdf'),
                #(".docx", 'docx'),
                (".txt", 'txt')
            ],
            'pptx': [
                #(".png", 'png'),
                #(".jpeg", 'jpeg'),
                #(".pdf", 'pdf'),
                #(".docx", 'docx'),
                (".txt", 'txt')
            ],
        },
    'download':
        {
            'youtube':
                [
                    ("Full video", 'full'),
                    ("Cut a piece", 'piece'),
                    ("Download a playlist", 'playlist'),
                    #("Cut audio from video", 'audio'),
                ],
            'instagram':
                [
                    ("Download a video", 'insta_video'),
                    #("Download a photo", 'insta_photo'),
                ],
            'tiktok':
                [
                    ("Download a video", 'tiktok_video'),
                ]
        }
}