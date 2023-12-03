import { Hero, HeroIllustration } from '@/components/hero'
import { Layout } from '@/components/layout'

export default function HomePage() {
  return (
    <Layout>
      <Hero
        title="Effortless Documentation for Your Software Project"
        content="Docify-AI is the ultimate solution for simplifying the process of creating in-depth documentation for your software projects. Our web application is designed to streamline the generation of descriptive documents, ensuring that your software project is thoroughly documented with ease."
        illustration={<HeroIllustration />}
      />
    </Layout>
  )
}
