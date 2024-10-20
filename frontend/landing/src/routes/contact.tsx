import { Article } from '@/components/article'
import { Layout } from '@/components/layout'
import { Link } from 'react-router-dom'

export default function ContactPage() {
  return (
    <Layout>
      <Article
        title="Contact"
        imageAlt="Lorem Picsum"
        imageSrc="https://picsum.photos/420/640?grayscale"
      >
        <p>Tabish Hassan</p>
        <p>
          Email: <Link to="mailto:tabishhassan1oo"> tabishhassan1oo@gmail.com</Link>
        </p>
      </Article>
    </Layout>
  )
}
