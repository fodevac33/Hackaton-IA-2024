import { clients } from "../data/clients";
import { useNavigate } from "react-router-dom";

export default function Index() {
  const navigate = useNavigate();

  const handleOnClick = (clientId: number) => {
    navigate(`/bot?clientId=${clientId}`);
  };
  return (
    <div className="h-screen w-full flex flex-col items-center p-6">
      <h1 className="text-6xl text-wrap font-bold text-blue-600">
        Elige el cliente que simularas
      </h1>
      <div className="grid lg:grid-cols-3 grid-cols-1 h-full w-full p-4 gap-8 mt-4">
        {clients.map((client, index) => {
          return (
            <div
              className="flex flex-col items-center border-4 rounded-xl border-blue-500 p-4 cursor-pointer hover:scale-105 shadow-md shadow-blue-500/40"
              onClick={() => handleOnClick(client.id)}
              key={index}
            >
              <h2 className="text-center text-2xl font-bold text-blue-800">
                {client.name}
              </h2>
              <img
                src={client.img}
                alt={`${client.name}'s profile`}
                className="rounded-full w-44 h-44 object-cover my-4"
              />
              <div className=" border-2 rounded-xl mt-auto w-full">
                <h1 className="text-xl font-semibold text-center text-blue-800">
                  Datos personales
                </h1>
                <div className="w-full flex justify-around mt-2">
                  <h2 className="font-semibold">Fecha de nacimiento:</h2>
                  <h2>{client.birth_date}</h2>
                </div>
                <div className="w-full flex justify-around mt-2">
                  <h2 className="font-semibold">ID:</h2>
                  <h2>{client.id_number}</h2>
                </div>
                <div className="w-full flex justify-around mt-2">
                  <h2 className="font-semibold">Phone:</h2>
                  <h2>{client.phone}</h2>
                </div>
                <div className="w-full flex justify-around mt-2">
                  <h2 className="font-semibold">Estado:</h2>
                  <h2 className="text-red-600">{client.status}</h2>
                </div>

                <div className="mt-6 w-full">
                  <h3 className="text-xl font-bold text-blue-600 text-center mb-2">
                    Pagos
                  </h3>
                  <div className="space-y-2">
                    {client.payments.map((pay, index) => (
                      <div
                        key={index}
                        className="flex justify-between bg-gray-100 rounded-lg p-3 text-gray-600"
                      >
                        <span className="font-semibold">Monto:</span>
                        <span>${pay.amount}</span>
                        <span className="font-semibold">Fecha:</span>
                        <span>{pay.date}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
