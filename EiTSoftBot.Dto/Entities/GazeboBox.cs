namespace EiTSoftBot.Dto.Entities
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
        double Weight);
}
