import { Article } from '@/components/article'
import { Layout } from '@/components/layout'

export default function FaqsPage() {
  return (
    <Layout>
      <Article
        title="FAQ's"
        imageAlt="Lorem Picsum"
        imageSrc="https://picsum.photos/420/640?grayscale"
      >
        <p>Add your FAQ content here.</p>
        <details
          className="mt-4 block rounded-sm border px-4 open:border-primary-400 hover:border-primary-300"
          open
        >
          <summary className="-mx-4 cursor-pointer border-primary-200 px-4 py-3">
            What is Docify-ai?
          </summary>
          <p>
            Docify-ai is a automatic documentation generator developed by{' '}
            <a href="https://twitter.com/tabish127001">@tabish127001</a>!
          </p>
        </details>
        {/*<details className="mt-4 block rounded-sm border border-gray-200 px-4 hover:border-primary-300">*/}
        {/*  <summary className="-mx-4 cursor-pointer px-4 py-3">How can I use Docify-ai?</summary>*/}
        {/*  <p>*/}
        {/*    Holly is licensed under the MIT License, which means you can use it for personal and*/}
        {/*    commercial projects for free.*/}
        {/*  </p>*/}
        {/*</details>*/}
        <details className="mt-4 block rounded-sm border border-gray-200 px-4 hover:border-primary-300">
          <summary className="-mx-4 cursor-pointer px-4 py-3">Can I see the code?</summary>
          <p>
            Yes, you can! Docify-ai is an open source project, and you can contribute to it on{' '}
            <a href="https://github.com/the-runtime/docify-ai">GitHub</a>.
          </p>
        </details>
      </Article>
    </Layout>
  )
}
