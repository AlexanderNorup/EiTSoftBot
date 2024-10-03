namespace EiTSoftBot
{
    /// <summary>
    /// This is a C# representation of the <c>box.js</c> class
    /// </summary>
    public record JsBox(string Id,
        double X, // Short side of mir
        double Y, // Long side of Mir
        double Z,
        double Width, // Along short side of MiR
        double Length, // Along long side of MiR
        double Height,
        double Weight)
    {
        public const double JsMirLength = 760; // Units in 2D scene
        public const double JsMirWidth = 450; // Units in 2D scene
    }
}
