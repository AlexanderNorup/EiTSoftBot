using EiTSoftBot.Dto.Entities;

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
        public const double MiRHeight = 0.36; // Meters
        public const double MiRLength = 0.757276; // Meters
        public const double MiRWidth = 0.440944; // Meters
        public const double CenterOfMiRLength = MiRLength / 2;
        public const double CenterOfMiRWidth = MiRWidth / 2;

        public const double MiR2DToRealWorldDimentions = MiRLength / JsBox.JsMirLength;

        public MujocoBox AsMujocoBox()
        {
            return new MujocoBox(
                Id: Id,
                X: Math.Round((Y + (Length / 2)) * MiR2DToRealWorldDimentions - CenterOfMiRLength, 3),
                Y: Math.Round((X + (Width / 2)) * MiR2DToRealWorldDimentions - CenterOfMiRWidth, 3),
                Z: Math.Round(((Z + (Height / 2)) * MiR2DToRealWorldDimentions) + MiRHeight, 3),
                SizeX: Math.Round(Length * MiR2DToRealWorldDimentions / 2, 3),
                SizeY: Math.Round(Width * MiR2DToRealWorldDimentions / 2, 3),
                SizeZ: Math.Round(Height * MiR2DToRealWorldDimentions / 2, 3),
                Weight: Weight);
        }
    }
}
