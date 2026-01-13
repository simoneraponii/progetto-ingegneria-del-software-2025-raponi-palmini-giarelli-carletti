import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from controller.rapporto_controller import RapportoController 
from model.enum.ruolo import Ruolo
from model.enum.stato_verbale import StatoVerbale

class TestRapportoController(unittest.TestCase):

    def setUp(self):
        self.controller = RapportoController()
        self.controller.rapporto_dao = MagicMock()

    @patch('controller.rapporto_controller.datetime')
    def test_genera_codice_protocollo_primo_anno(self, mock_datetime):
        #oggi siamo nel 2024
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        #e non ci sono verbali per quest anno (per ora)
        self.controller.rapporto_dao.get_protocolli_by_anno.return_value = []
        codice = self.controller.genera_codice_protocollo()
        self.assertEqual(codice, "001/24")
        self.controller.rapporto_dao.get_protocolli_by_anno.assert_called_with("24")

    @patch('controller.rapporto_controller.datetime')
    def test_genera_codice_protocollo_incrementale(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 5, 10)
        #facciamo finta di avere questi protocolli
        self.controller.rapporto_dao.get_protocolli_by_anno.return_value = [
            "001/24", "002/24", "015/24"
        ]
        codice = self.controller.genera_codice_protocollo()
        #mi aspetto 16
        self.assertEqual(codice, "016/24")


    def test_crea_verbale(self):

        # no protocolli per quest anno
        self.controller.rapporto_dao.get_protocolli_by_anno.return_value = []
        self.controller.rapporto_dao.insert_verbale.return_value = True
        result = self.controller.crea_verbale("Rissa in cella", "MAT123")
        self.assertTrue(result)
        # verifico che insert_verbale sia stato chiamato. 
        self.controller.rapporto_dao.insert_verbale.assert_called()
        args = self.controller.rapporto_dao.insert_verbale.call_args[0]
        self.assertEqual(args[1], "Rissa in cella")
        self.assertEqual(args[2], "MAT123")

    def test_conferma_verbale_comandante(self):
        #controllo se la conferma verbale del comandante è corretta
        self.controller.rapporto_dao.update_stato_verbale.return_value = True
        result = self.controller.conferma_verbale("123/24", Ruolo.COMANDANTE)
        self.assertTrue(result)
        self.controller.rapporto_dao.update_stato_verbale.assert_called_with(
            "123/24", StatoVerbale.CONFIRMED_COMANDANTE
        )

    def test_conferma_verbale_ufficio_comando(self):
        #controllo se la conferma verbale del comandante è corretta
        self.controller.rapporto_dao.update_stato_verbale.return_value = True
        result = self.controller.conferma_verbale("123/24", Ruolo.UFFICIO_COMANDO)
        self.assertTrue(result)
        self.controller.rapporto_dao.update_stato_verbale.assert_called_with(
            "123/24", StatoVerbale.CONFIRMED_UFFICIO_COMANDO
        )

    def test_conferma_verbale_ruolo_sbagliato(self):
        # ruolo fittizio che non puo confermare
        FAKE_ROLE = MagicMock() 
        self.controller.conferma_verbale("123/24", FAKE_ROLE)
        self.controller.rapporto_dao.update_stato_verbale.assert_called_with(
            "123/24", None
        )




if __name__ == '__main__':
    unittest.main()