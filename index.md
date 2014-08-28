---
layout: homepage
---
<core-style ref="rw-theme"></core-style>
<core-style ref="tile-layout"></core-style>

<core-scroll-header-panel flex class="theme dark bluegrey bg fg">
  <core-toolbar class="theme bluegrey bg fg">
    <div flex>{{ site.title }}</div>
  </core-toolbar>

  <div content>
    <nav style="padding: 8px;" horizontal layout center-justified>
      <card-container tile w12 style="max-width: 1400px;">
        <card-container tile w12 h3 md-w6 md-h6 lg-w6 lg-h8>
          <section-card tile w6 h3 md-w12 md-h4 lg-h6 featured
            label="{{ site.posts[0].title }}" theme="blue"
            coverSrc="{{sit.url}}/{{ site.posts[0].cover }}"
            href="{{ site.posts[0].url }}"></section-card>
          <section-card tile w6 h1 md-w12 icon="communication:message" theme="blue"
            href="{{ site.posts[1].url }}"
            label="{{ site.posts[1].title }}"></section-card>
          <section-card tile w6 h1 icon="communication:message" theme="blue"
            href="{{ site.posts[2].url }}"
            label="{{ site.posts[2].title }}"></section-card>
          <section-card tile w6 h1 icon="more-horiz" theme="blue" href="/articles"
            label="More articles"></section-card>
        </card-container>

        <card-container tile w12 h6 md-w6 md-h6 lg-w6 lg-h8>
          <section-card tile w6 h3 md-h3 lg-h4 featured label="Software" icon="rw:software" theme="purple"
            href="/software"></section-card>
          <section-card tile w6 h3 md-h3 lg-h4 featured label="Publications" icon="rw:publications" theme="indigo"
            href="/publications"></section-card>
          <section-card tile w6 h3 md-h3 lg-h4 featured label="Research" icon="rw:research" theme="green"
            href="/research"></section-card>
          <section-card tile w6 h3 md-h3 lg-h4 featured label="Teaching" icon="rw:teaching" theme="cyan"
            href="/teaching"></section-card>
        </card-container>

        <card-container tile w12 h2 md-w6 lg-w6 lg-h2>
          <section-card tile w6 h1 lg-w6 icon="rw:github" theme="deeporange" label="Github"
            href="https://github.com/rjw57"></section-card>
          <section-card tile w6 h1 lg-w6 icon="google-plus" theme="deeporange" label="Google Plus"
            href="https://google.com/+RichWareham"></section-card>
          <section-card tile w6 h1 lg-w6 icon="rw:twitter" theme="deeporange" label="Twitter"
            href="https://twitter.com/richwareham"></section-card>
          <section-card tile w6 h1 lg-w6 icon="rw:facebook" theme="deeporange" label="Facebook"
            href="https://facebook.com/profile.php?id=100008218691466"></section-card>
        </card-container>

        <card-container tile w12 h2 md-w6 lg-w3>
          <section-card tile w12 h1 icon="communication:message" theme="teal" href="/contact"
            label="Contact information"></section-card>
          <section-card tile w12 h1 icon="list" theme="teal" href="/cv"
            label="Curriculum Vitæ"></section-card>
        </card-container>

        <card-container tile w12 h1 lg-w3 lg-h2>
          <section-card tile w6 h1 lg-w12 icon="help" href="/about"
            label="About Rich"></section-card>
          <section-card tile w6 h1 lg-w12 icon="link" href="/links"
            label="Links"></section-card>
        </card-container>
      </card-container>
    </nav>
  </div>
</core-scroll-header-panel>
