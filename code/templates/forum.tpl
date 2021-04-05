<main class="forum-body">
   
    
    
%for post in posts:

    <article class ="post">
        <header>
            <div>
                <h1>{{post['title']}}</h1>
                <div class="about">{{post['author_id']}}</div>
            </div>
        </header>
            <p class="body"> {{post['body']}}</p>
    </article>

%end
</main>
