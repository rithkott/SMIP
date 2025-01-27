export default async function RSLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return(
        <div className="animate-appear">
            {children}
        </div>
    )
}