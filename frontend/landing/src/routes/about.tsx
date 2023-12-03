import { Article } from '@/components/article'
import { Layout } from '@/components/layout'

function AboutPage() {
  return (
    <Layout>
      <Article
        title="About"
        imageAlt="Lorem Picsum"
        imageSrc="https://picsum.photos/420/640?grayscale"
      >
        {/* prettier-ignore */}
        <p>
            Docify-ai is a automatic documentation generator developed by <a href="https://twitter.com/tabish127001">@tabish127001</a>!
          </p>
        <p>
          This is a personal project, and it's still in the early stages of development. As such,
          it's not yet recommended for production use.
        </p>
      </Article>
    </Layout>
  )
}

export default AboutPage
