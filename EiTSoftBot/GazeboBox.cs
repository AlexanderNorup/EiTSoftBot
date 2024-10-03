namespace EiTSoftBot
{
    /// <summary>
    /// Gazebo representation of box. <br>
    /// Size and position measurements are in Meters. <br>
    /// Weight is in Kilograms. <br>
    /// A box is positioned from the center of itself.
    /// </summary>
    public record GazeboBox(string Id,
        double X, // Long side of MiR (positive towards front). 0=center
        double Y, // Short side of MiR (positive towards left). 0=center
        double Z, // Height of box 0=top of MiR
        double SizeX, // = Length
        double SizeY, // = Width
        double SizeZ, // = Height
        double Weight)
    {
        public const double MiRLength = 0.89; // Meters
        public const double MiRWidth = 0.58; // Meters
        public const double CenterOfMiRLength = MiRLength / 2;
        public const double CenterOfMiRWidth = MiRWidth / 2;

        public const double MiR2DToRealWorldDimentions = MiRLength / JsBox.JsMirLength;

        public static GazeboBox FromJsBox(JsBox box)
        {
            return new GazeboBox(
                Id: box.Id,
                X: ((box.Y - (box.Length / 2)) * MiR2DToRealWorldDimentions) - CenterOfMiRLength,
                Y: ((box.X - (box.Width / 2)) * MiR2DToRealWorldDimentions) - CenterOfMiRWidth,
                Z: (box.Z - (box.Height / 2)) * MiR2DToRealWorldDimentions,
                SizeX: box.Length * MiR2DToRealWorldDimentions,
                SizeY: box.Width * MiR2DToRealWorldDimentions,
                SizeZ: box.Height * MiR2DToRealWorldDimentions,
                Weight: box.Weight);
        }
    }
}
